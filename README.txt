Open index.html in a browser to view the static site. For full functionality (CSV download) open it via a local static server, e.g. from the folder run:

python3 -m http.server 8000

Then visit http://localhost:8000

To show your webpassport image: create a folder named images in the same directory and place webpassport.png there (path: images/webpassport.png). The index.html will use that local file if present and otherwise fall back to an online placeholder image.

If you used the Python drafter app and have the image at /mnt/data/images/webpassport.png, copy or move it into images/webpassport.png in this project folder so the static site can display it.
