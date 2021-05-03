module.exports = {
  future: {
    webpack5: true,
  },
  images: {
    loader: "imgix",
  },
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    return config;
  },
};
