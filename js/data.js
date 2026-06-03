const DATA = {
  years: ['2021-22','2022-23','2023-24','2024-25','2025-26','2026-27*'],

  elephantDeaths: [4, 12, 6, 10, 12, 4],
  humanDeaths: [13, 1, 7, 8, 16, 0],

  divisionTotals: {
    dh: { human: 36, elephant: 27 },
    rg: { human: 9, elephant: 21 }
  },

  causeOfDeath: [
    { cause: 'Electrocution', count: 23, pct: 48 },
    { cause: 'Suspected Drowning', count: 12, pct: 25 },
    { cause: 'Natural / Old Age', count: 4, pct: 8 },
    { cause: 'Fall / Trauma', count: 4, pct: 8 },
    { cause: 'Other', count: 5, pct: 10 }
  ],

  ageProfile: [
    { group: 'Calf (0–2 yr)',      count: 22, pct: 49 },
    { group: 'Juvenile (2–15 yr)', count: 5,  pct: 11 },
    { group: 'Sub-adult (15–30 yr)', count: 2, pct: 4 },
    { group: 'Adult (30–55 yr)',   count: 11, pct: 24 },
    { group: 'Old (55+ yr)',       count: 5,  pct: 11 }
  ],

  sexProfile: { male: 23, female: 22, unknown: 0 },  // 45 total

  // Exact monthly distribution from detailed records
  seasonal: {
    months: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    counts: [6, 4, 3, 2, 5, 4, 1, 1, 3, 8, 6, 5]
  },

  rangeWise: [
    { beat: 'Ghargoda (RG)', count: 15, div: 'Raigarh', risk: 'CRITICAL' },
    { beat: 'Chhal (DH)', count: 10, div: 'Dharamjaigarh', risk: 'CRITICAL' },
    { beat: 'Dharamjaigarh HQ', count: 7, div: 'Dharamjaigarh', risk: 'HIGH' },
    { beat: 'Tamanar (RG)', count: 5, div: 'Raigarh', risk: 'MODERATE' },
    { beat: 'Borojh (DH)', count: 4, div: 'Dharamjaigarh', risk: 'HIGH' },
    { beat: 'Lailungaan (DH)', count: 2, div: 'Dharamjaigarh', risk: 'HIGH' },
    { beat: 'Baakaaruma (DH)', count: 1, div: 'Dharamjaigarh', risk: 'MODERATE' },
    { beat: 'Raigarh HQ', count: 1, div: 'Raigarh', risk: 'LOW' }
  ],

  // All 90 geo-points [lat, lon, cause/village, year]
  geoPoints: {
    dhHuman: [
      [22.408, 83.187, 'Krondha', '2021-22'],
      [22.347, 83.237, 'Gersa', '2021-22'],
      [22.449, 83.114, 'Koylar', '2021-22'],
      [22.774, 83.165, 'Anchira', '2021-22'],
      [22.774, 83.165, 'Anchira', '2021-22'],
      [22.582, 83.171, 'Balpeda', '2021-22'],
      [22.700, 83.046, 'Ongna', '2021-22'],
      [22.414, 83.264, 'Ongna', '2021-22'],
      [22.731, 83.137, 'Jaldega', '2021-22'],
      [22.434, 83.191, 'Taraimaur', '2021-22'],
      [22.687, 83.272, 'Ratnpur', '2021-22'],
      [22.710, 83.258, 'Gidhkalo', '2021-22'],
      [22.236, 83.279, 'Bojiya', '2023-24'],
      [22.140, 83.123, 'Chhal', '2023-24'],
      [22.313, 83.091, 'Chhal', '2023-24'],
      [22.086, 83.161, 'Chhal', '2023-24'],
      [22.588, 83.998, 'Pakargaon', '2023-24'],
      [22.440, 83.264, 'Hati', '2024-25'],
      [22.185, 83.179, 'Auranaara', '2024-25'],
      [22.338, 83.196, 'Kudekela', '2024-25'],
      [22.750, 83.543, 'Tejpur', '2024-25'],
      [22.406, 83.141, 'Koylar', '2024-25'],
      [22.631, 83.243, 'Balpeda', '2024-25'],
      [22.4995, 83.4307, 'Baguadega', '2024-25'],
      [22.612, 83.766, 'Amapali', '2024-25'],
      [22.617, 84.022, 'Pakargaon', '2025-26'],
      [22.618, 84.025, 'Pakargaon', '2025-26'],
      [22.393, 83.227, 'Amgaon', '2025-26'],
      [22.5144, 83.4287, 'Rairuma', '2025-26'],
      [22.365, 83.550, 'Lailenga', '2025-26'],
      [22.365, 83.545, 'Rajaaama', '2025-26'],
      [22.372, 83.804, 'Rajaaama', '2025-26'],
      [22.4056, 83.170, 'Krondha', '2025-26'],
      [22.631, 83.243, 'Khambhar(N)', '2025-26'],
      [22.440, 83.264, 'Chhal', '2025-26'],
      [22.762, 83.323, 'Kapu', '2025-26']
    ],
    dhElephant: [
      [22.198, 83.166, 'Electrocution', '2021-22'],
      [22.589, 83.101, 'Natural death', '2021-22'],
      [22.397, 83.257, 'Electrocution', '2021-22'],
      [22.770, 83.171, 'Fall from hill', '2021-22'],
      [22.320, 83.752, 'Lightning strike', '2022-23'],
      [22.688, 83.534, 'Lightning strike', '2022-23'],
      [22.688, 83.534, 'Electrocution', '2022-23'],
      [22.648, 83.496, 'Old age/fall from hill', '2022-23'],
      [22.611, 83.412, 'Electrocution', '2022-23'],
      [22.355, 83.413, 'Natural/old age', '2022-23'],
      [22.174, 83.152, 'Electrocution', '2023-24'],
      [22.290, 83.146, 'Inter-elephant conflict', '2023-24'],
      [22.731, 83.321, 'Electrocution', '2023-24'],
      [22.729, 83.235, 'Electrocution', '2023-24'],
      [22.445, 83.153, 'Electrocution', '2023-24'],
      [22.580, 83.241, 'Electrocution', '2023-24'],
      [22.259, 83.173, 'Calf death at birth', '2024-25'],
      [22.660, 83.354, 'Tusk injury', '2024-25'],
      [22.322, 83.096, 'Suspected Drowning in pond', '2024-25'],
      [22.373, 83.151, 'Electrocution', '2024-25'],
      [22.259, 83.146, 'Natural death', '2024-25'],
      [22.284, 83.137, 'Suspected Drowning in pond', '2024-25'],
      [22.166, 83.173, 'Suspected Drowning in pond', '2025-26'],
      [22.359, 83.452, 'Cardiovascular shock (undetermined)', '2026-27'],
      [22.146, 83.212, 'Suspected Drowning in pond', '2026-27'],
      [22.166, 83.115, 'Suspected Drowning (asphyxia)', '2026-27'],
      [22.100, 83.159, 'Suspected Drowning in pond', '2026-27']
    ],
    rgHuman: [
      [22.113, 83.350, 'Samaruma', '2021-22'],
      [22.455, 83.646, 'Pora', '2022-23'],
      [22.455, 83.646, 'Baturaachhar', '2022-23'],
      [22.121, 83.222, 'Kafarmaar', '2022-23'],
      [22.096, 83.708, 'Kaantajharia', '2023-24'],
      [22.069, 83.373, 'Jhingol', '2024-25'],
      [22.126, 83.266, 'Tendumudi', '2024-25'],
      [22.497, 83.585, 'Baraud', '2024-25'],
      [22.170, 83.388, 'DehriDih', '2025-26']
    ],
    rgElephant: [
      [22.245, 83.414, 'Heatstroke', '2022-23'],
      [22.215, 83.470, 'Electrocution', '2022-23'],
      [22.165, 83.510, 'Electrocution', '2022-23'],
      [22.090, 83.420, 'Sun stroke', '2022-23'],
      [22.179, 83.518, 'Electrocution', '2022-23'],
      [22.498, 83.501, 'Electrocution', '2022-23'],
      [22.218, 83.564, 'Electrocution(3)', '2024-25'],
      [22.104, 83.243, 'Suspected Drowning-Panikshet dam', '2024-25'],
      [22.198, 83.468, 'Suspected Drowning-Rabo dam', '2024-25'],
      [22.102, 83.241, 'Suspected Drowning-Panikshet dam', '2024-25'],
      [22.211, 83.470, 'Brain injury', '2025-26'],
      [22.152, 83.494, 'Suspected Drowning', '2025-26'],
      [22.202, 83.418, 'Electrocution', '2025-26'],
      [22.021, 83.332, 'Suspected Drowning', '2025-26'],
      [21.985, 83.462, 'Suspected Drowning', '2025-26'],
      [22.555, 83.615, 'Fell in nala', '2025-26'],
      [22.065, 83.392, 'Weakness', '2025-26'],
      [22.181, 83.455, 'Electrocution(2)', '2025-26']
    ]
  },

  populationTrend: {
    years: ['2001','2005','2007','2015','2017','2021','2026'],
    cg:   [24, 123, 122, 247, 247, 279, 451]
  }
};
