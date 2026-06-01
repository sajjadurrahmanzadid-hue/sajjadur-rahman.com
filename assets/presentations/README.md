# assets/presentations/

Drop your downloadable files here — conference papers, presentation slides, posters.
The file is served statically by GitHub Pages at:
  https://sajjadur-rahman.com/assets/presentations/your-filename.pdf

## Naming convention

Use the same slug pattern as presentations.json entries:

  [year]-[short-topic]-[type].[ext]

Examples:
  2025-nano-fertilizer-wheat-slides.pdf
  2024-ait-hydroponics-paper.pdf
  2024-ege-iot-agriculture-proceedings.pdf
  2024-sustainable-ag-poster.pdf

## To link a file on the site

1. Add the file to this folder and commit to GitHub.
2. Open assets/data/presentations.json.
3. Find the matching entry by "id".
4. Set "file" to the path:
     "file": "assets/presentations/2025-nano-fertilizer-wheat-slides.pdf"
5. Set "file_type" to one of:
     "paper"  → button shows "Download Paper"
     "slides" → button shows "Download Slides"
     "poster" → button shows "Download Poster"
6. Commit. The download button appears automatically on research.html.

## Multiple files per presentation

If you have both a paper AND slides for the same presentation,
add a second entry in presentations.json with the same conference
details but different "file" and "file_type" values,
and set "show_separately": true.
