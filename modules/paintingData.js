const artist = "Dendi A.R. Kadmaerubun";

export const paintingData = [
  {
    imgSrc: `${import.meta.env.BASE_URL}artworks/1.jpg`,
    width: 5,
    height: 3,
    position: { x: -10, y: 2, z: -19.5 },
    rotationY: 0,
    info: {
      title: "stensil potret ",
      artist,
      description: "stensil karakter Papua",
      year: "2023",
    },
  },
  {
    imgSrc: `${import.meta.env.BASE_URL}artworks/2.jpg`,
    width: 5,
    height: 3,
    position: { x: 0, y: 2, z: -19.5 },
    rotationY: 0,
    info: {
      title: "Colase poster",
      artist,
      description: "Melestarikan culture Papua",
      year: "2025",
    },
  },
  {
    imgSrc: `${import.meta.env.BASE_URL}artworks/3.jpg`,
    width: 5,
    height: 3,
    position: { x: 10, y: 2, z: -19.5 },
    rotationY: 0,
    info: {
      title: "Alama Papua",
      artist,
      description: "Kampanye sosial, tentang menjaga habitat herbivora Papua",
      year: "2025",
    },
  },
  {
    imgSrc: `${import.meta.env.BASE_URL}artworks/4.jpg`,
    width: 5,
    height: 3,
    position: { x: -10, y: 2, z: 19.5 },
    rotationY: Math.PI,
    info: {
      title: "poster kampanye",
      artist,
      description: "kampanye sosial, tentang penyalahgunaan ganja",
      year: "2025",
    },
  },
  {
    imgSrc: `${import.meta.env.BASE_URL}artworks/5.jpg`,
    width: 5,
    height: 3,
    position: { x: 0, y: 2, z: 19.5 },
    rotationY: Math.PI,
    info: {
      title: "karya cetak tinggi",
      artist,
      description: "Dari tumbuhan liar",
      year: "2023",
    },
  },
  {
    imgSrc: `${import.meta.env.BASE_URL}artworks/6.jpg`,
    width: 5,
    height: 3,
    position: { x: 10, y: 2, z: 19.5 },
    rotationY: Math.PI,
    info: {
      title: "poster",
      artist,
      description: "keterikatan Culture",
      year: "2026",
    },
  },
];
