import Head from "next/head";

export default function Home() {
  return (
    <>
      <Head>
        <title>Mario-César Señoranis</title>
        <meta name="viewport" content="width=device-width"></meta>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <header></header>
      <div className="container">
        <main>
          <h1>Hello, I’m Mario&minus;César Señoranis</h1>
          <p>
            I’m a software developer, trying to write, create and mostly being a
            great father
          </p>
        </main>
      </div>
    </>
  );
}
