// Drive the learning section in real Chrome (headless) and assert it works.
const puppeteer = require("puppeteer-core");
const path = require("path");
const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL = "file:///" + path.join(__dirname, "..", "index.html").replace(/\\/g, "/");
const SHOT = p => path.join(__dirname, "raw", p);

function assert(cond, msg){ if(!cond){ console.error("ASSERT FAILED:", msg); process.exitCode = 1; throw new Error(msg); } }

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: "new",
    args: ["--allow-file-access-from-files", "--no-sandbox"] });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1100, height: 1400, deviceScaleFactor: 1 });
  const errs = [];
  pg.on("pageerror", e => errs.push(String(e)));
  pg.on("console", m => { if (m.type() === "error") errs.push("console:" + m.text()); });
  await pg.goto(URL, { waitUntil: "networkidle0" });

  // enter learn mode
  await pg.click("#learnEntry");
  await pg.waitForSelector("#screen-learn:not(.hidden)");
  await pg.waitForSelector("#learnToc button");

  const tocCount = await pg.$$eval("#learnToc button", els => els.length);
  assert(tocCount === 16, "expected 16 chapters in TOC, got " + tocCount);

  const firstTitle = await pg.$eval(".learn-h", e => e.textContent.trim());
  assert(firstTitle.length > 0, "first chapter has a title");
  await pg.screenshot({ path: SHOT("learn-intro.png") });

  // jump to a chapter that has images + a table is elsewhere; first verify ch9 table
  // click chapter 10 (index 10 -> ch9? ids: intro,ch1..ch13,cheat,principles) find by text
  async function goToTitleContaining(sub){
    const i = await pg.$$eval("#learnToc button", (els, s) =>
      els.findIndex(e => e.textContent.includes(s)), sub);
    assert(i >= 0, "TOC entry containing '" + sub + "' exists");
    await pg.evaluate(i => document.querySelectorAll("#learnToc button")[i].click(), i);
  }

  // chapter 9 has the confusion-matrix table
  await goToTitleContaining("פרק 9");
  await pg.waitForFunction(() => document.querySelector(".learn-content table") !== null);
  const hasTable = await pg.$eval(".learn-content", e => !!e.querySelector("table"));
  assert(hasTable, "ch9 renders a table");

  // chapter 10 has 4 figures — verify every image actually loaded
  await goToTitleContaining("פרק 10");
  await pg.waitForSelector(".learn-fig img");
  await pg.waitForFunction(() => {
    const imgs = [...document.querySelectorAll(".learn-content img")];
    return imgs.length > 0 && imgs.every(im => im.complete);
  }, { timeout: 8000 });
  const imgStats = await pg.$$eval(".learn-content img", els =>
    els.map(im => ({ src: im.getAttribute("src"), w: im.naturalWidth })));
  assert(imgStats.length >= 3, "ch10 has multiple figures");
  imgStats.forEach(s => assert(s.w > 0, "image failed to load: " + s.src));
  await pg.screenshot({ path: SHOT("learn-ch10.png") });

  // lightbox open/close
  await pg.click(".learn-fig img");
  await pg.waitForSelector("#lightbox:not(.hidden)");
  const lbSrc = await pg.$eval("#lightboxImg", e => e.getAttribute("src"));
  assert(lbSrc && lbSrc.includes("images/"), "lightbox shows an image");
  await pg.screenshot({ path: SHOT("learn-lightbox.png") });
  await pg.click("#lightboxClose");
  await pg.waitForSelector("#lightbox.hidden");

  // prev/next navigation
  const posBefore = await pg.$eval("#learnPos", e => e.textContent.trim());
  await pg.click("#learnNext");
  const posAfter = await pg.$eval("#learnPos", e => e.textContent.trim());
  assert(posBefore !== posAfter, "next button advances chapter");

  // back to home
  await pg.click("#learnBackBtn");
  await pg.waitForSelector("#screen-start:not(.hidden)");

  // light theme screenshot of learn for visual review
  await pg.evaluate(() => { document.documentElement.dataset.theme = "light"; });
  await pg.click("#learnEntry");
  await pg.waitForSelector("#screen-learn:not(.hidden)");
  await goToTitleContaining("פרק 6");
  await pg.waitForSelector(".learn-fig img");
  await pg.waitForFunction(() => [...document.querySelectorAll(".learn-content img")].every(im => im.complete));
  await pg.screenshot({ path: SHOT("learn-light-ch6.png") });

  // ---- mobile: drawer must be hidden by default, slide in on toggle ----
  await pg.evaluate(() => { document.documentElement.dataset.theme = "dark"; });
  await pg.setViewport({ width: 390, height: 780, deviceScaleFactor: 2 });
  await pg.reload({ waitUntil: "networkidle0" });
  await pg.click("#learnEntry");
  await pg.waitForSelector("#screen-learn:not(.hidden)");

  const vw = 390;
  const offRight = await pg.$eval("#learnToc", el => el.getBoundingClientRect().left);
  assert(offRight >= vw - 2, "TOC drawer is off-screen by default (left=" + Math.round(offRight) + ", vw=" + vw + ")");
  const backdropHidden = await pg.$eval("#learnBackdrop", el => el.classList.contains("hidden"));
  assert(backdropHidden, "backdrop hidden by default");
  await pg.screenshot({ path: SHOT("learn-mobile-closed.png") });

  // open the drawer
  await pg.click("#learnTocToggle");
  await new Promise(r => setTimeout(r, 350)); // allow slide transition
  const openLeft = await pg.$eval("#learnToc", el => el.getBoundingClientRect().left);
  assert(openLeft < vw - 100, "TOC drawer slides into view on toggle (left=" + Math.round(openLeft) + ")");
  const backdropShown = await pg.$eval("#learnBackdrop", el => !el.classList.contains("hidden"));
  assert(backdropShown, "backdrop shown when drawer open");
  await pg.screenshot({ path: SHOT("learn-mobile-open.png") });

  // tap backdrop closes
  await pg.click("#learnBackdrop");
  await new Promise(r => setTimeout(r, 350));
  const closedAgain = await pg.$eval("#learnToc", el => el.getBoundingClientRect().left);
  assert(closedAgain >= vw - 2, "backdrop tap closes drawer");

  // selecting a chapter from the drawer closes it too
  await pg.click("#learnTocToggle");
  await new Promise(r => setTimeout(r, 350));
  await pg.evaluate(() => document.querySelector("#learnToc button").click());
  await new Promise(r => setTimeout(r, 350));
  const afterPick = await pg.$eval("#learnToc", el => el.getBoundingClientRect().left);
  assert(afterPick >= vw - 2, "picking a chapter closes the drawer");
  await pg.screenshot({ path: SHOT("learn-mobile-content.png") });

  console.log("mobile drawer    : off-screen by default, slides in, closes on backdrop/pick");
  console.log("TOC chapters     :", tocCount);
  console.log("ch10 images      :", imgStats.length, "all loaded:", imgStats.every(s => s.w > 0));
  console.log("nav pos          :", posBefore, "->", posAfter);
  console.log("page errors      :", errs.length ? errs.join("\n") : "none");
  await b.close();
  assert(errs.length === 0, "no page/console errors");
  console.log("\nLEARN VERIFY PASSED");
})().catch(e => { console.error(e); process.exit(1); });
