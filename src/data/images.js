// React Native bundles images via static require() calls, so we map each
// bookmark image filename to its required asset here.
const IMAGES = {
  'bookmark1.png': require('../../assets/bookmark1.png'),
  'bookmark2.png': require('../../assets/bookmark2.png'),
  'bookmark4.png': require('../../assets/bookmark4.png'),
  'bookmark6.png': require('../../assets/bookmark6.png'),
  'bookmark7.png': require('../../assets/bookmark7.png'),
  'bookmark8.png': require('../../assets/bookmark8.png'),
  'bookmark9.png': require('../../assets/bookmark9.png'),
  'bookmark11.png': require('../../assets/bookmark11.png'),
  'bookmark12.png': require('../../assets/bookmark12.png'),
};

export function getBookmarkImage(filename) {
  return IMAGES[filename];
}

export default IMAGES;
