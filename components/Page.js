import Head from "next/head";

export default function Container({ children }) {
  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="robots" content="follow, index" />
        <meta
          name="description"
          content="I’m a software developer working at Zapier.com, here is my Personal site and Blog."
        />
        <meta
          name="keywords"
          content="python, bolivia, mariocesar, mariocesar_bo, zapier, software engineer"
        />
        <meta name="author" content="Mario-César Señoranis" />
        <link rel="canonical" itemProp="url" href="https://mariocesar.xyz/" />
        <link rel="author" href="https://mariocesar.xyz" />
        <meta
          property="og:title"
          content="Mario-César Señoranis Personal Website &amp; Blog"
        />
        <meta property="og:url" content="https://mariocesar.xyz" />
        <meta
          property="og:site_name"
          itemProp="name"
          content="Mario-César Señoranis Personal Website &amp; Blog"
        />
        <meta property="og:type" content="blog" />
        <meta content="#ffffff" name="theme-color" />
        <meta content="#ffffff" name="msapplication-TileColor" />
      </Head>
      <header />
      <main role="main">
        <div className="container">{children}</div>
      </main>
    </>
  );
}
