# Portfolio

Personal portfolio site and project source code.

## Structure

```
index.html               Home
resume.html               CV
skills.html                Skills
projects.html              Selected Work (project list)
contact.html                Contact
style.css                Shared stylesheet
resume.pdf               Public CV (download button on the CV page)
assets/                  Images used across the site
projects/
  options-pricer/
    index.html           Project write-up
  thai-algo-trading/
    index.html           Project write-up
  bank-stress-test/
    index.html           Project write-up
  lamphun-ndvi/
    index.html           Project write-up
    README.md            Project-specific readme (methodology, results)
    requirements.txt
    src/                 Cleaned Python source for the analysis
```

## Before you push this

A few things worth doing before this goes live:

1. **Replace the placeholder contact links** on every page's footer
   (`your.email@example.com`, `github.com/yourusername`,
   `linkedin.com/in/yourusername`) with your real ones.
2. **Add an actual `resume.pdf`** to the root folder. The CV page
   links to `resume.pdf` for the "Download CV (PDF)" button, but no
   file is included yet.
3. **Add your remaining figures.** The Lamphun project page currently
   uses your real satellite composite as the hero image. Your
   classification map (with the brown/green legend) and your final
   change-detection map (the red-highlighted conversion overlay)
   aren't in this bundle since they were generated on your own
   machine, drop them into `assets/` and reference them from
   `projects/lamphun-ndvi/index.html` alongside the existing figure.
4. **Fill in the Anime Recommender entry** on `projects.html` once it
   has real results, or remove it for now if you'd rather launch with
   just the one finished project.

## Running locally

This is a static site, no build step. Open `index.html` directly in a
browser, or serve it locally:

```
python -m http.server 8000
```

then visit `http://localhost:8000`.

## Deploying to GitHub Pages

1. Push this folder to a GitHub repository (e.g. `yourusername.github.io`
   for a root-level site, or any repo name for a project site).
2. In the repo's Settings → Pages, set the source to your main branch,
   root folder.
3. GitHub will publish it at `https://yourusername.github.io/` (or
   `https://yourusername.github.io/reponame/` for a project site).

```bash
git init
git add .
git commit -m "Initial portfolio"
git branch -M main
git remote add origin https://github.com/yourusername/yourrepo.git
git push -u origin main
```
