import Head from "next/head";

export default function Container({ children }) {
  const title = "Mario-César Señoranis Personal Website &amp; Blog";
  const description =
    "I’m a software developer here is my Personal site and Blog.";
  const siteurl = "https://mariocesar.xyz";

  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="robots" content="follow, index" />
        <meta name="description" content={description} />
        <meta
          name="keywords"
          content="python, bolivia, mariocesar, mariocesar_bo, zapier, software engineer"
        />
        <meta name="author" content="Mario-César Señoranis" />
        <link rel="canonical" itemProp="url" href={siteurl} />
        <link rel="author" href={siteurl} />

        <meta property="og:title" content={title} />
        <meta property="og:locale" content="en" />
        <meta property="og:url" content={siteurl} />
        <meta property="og:site_name" itemProp="name" content={title} />
        <meta property="og:type" content="blog" />
        <meta property="og:description" content={description} />
        <meta property="article:publisher" content={siteurl} />

        <meta name="twitter:site" content="@mariocesar_bo" />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />

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
