import Document, { Html, Head, Main, NextScript } from "next/document";

class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head itemtype="http://schema.org/Blog" itemscope="">
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <meta name="robots" content="follow, index" />

          <link rel="icon" href="/favicon.ico" />
          <meta
            name="description"
            content="I’m a software developer working at Zapier.com, here is my Personal site and Blog."
          />
          <meta
            name="keywords"
            content="python, bolivia, mariocesar, mariocesar_bo, zapier, software engeineer"
          />
          <meta name="author" content="Mario-César Señoranis" />

          <link rel="canonical" itemprop="url" href="https://mariocesar.xyz/" />
          <link rel="author" href="https://mariocesar.xyz" />

          <meta property="og:title" content="" />
          <meta property="og:url" content="https://mariocesar.xyz" />
          <meta
            property="og:site_name"
            itemprop="name"
            content="Mario-César Señoranis Personal Website &amp; Blog"
          />
          <meta property="og:type" content="blog" />

          <meta content="#ffffff" name="theme-color" />
          <meta content="#ffffff" name="msapplication-TileColor" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
