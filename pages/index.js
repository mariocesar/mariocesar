import Head from "next/head";

const ListItem = ({ icon, children }) => {
  return (
    <li data-icon={icon}>
      <span>{children}</span>
    </li>
  );
};

const MarkupLink = ({ href }) => {
  return (
    <a target="_blank" href={href}>
      {href}
    </a>
  );
};

export default function Home() {
  return (
    <>
      <Head>
        <title>Mario-César Señoranis</title>
        <meta name="viewport" content="width=device-width"></meta>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <header></header>
      <main>
        <div className="container">
          <h1>
            👋🏼 Hello,
            <br />
            I’m Mario&minus;César Señoranis
          </h1>
          <p>
            I’m a software developer, trying to write, create, and mostly being
            a great father. I work at ⚡️
            <MarkupLink href="https://zapier.com/" /> as an Integration Software
            Engineer. You’ve found my slice of the internet.
          </p>
          <p>You can also find me:</p>
          <ul role="list">
            <ListItem icon="🧑🏽‍💻">
              Talking about work in LinkedIn{" "}
              <MarkupLink href="https://www.linkedin.com/in/mariocesar/" />
            </ListItem>

            <ListItem icon="📸">
              Sharing pretty photos at Instagram{" "}
              <MarkupLink href="https://instagram.com/mariocesar_bo/" />
            </ListItem>
            <ListItem icon="🎉">
              Speaking in Clubhouse{" "}
              <MarkupLink href="https://www.joinclubhouse.com/@mariocesar" />
              <ul role="list">
                <ListItem icon="☕">
                  I host a room in the club "Club del Desayuno" every day at 9
                  am about Accountability and Networking. See{" "}
                  <MarkupLink href="https://www.joinclubhouse.com/club/club-del-desayuno" />
                </ListItem>
              </ul>
            </ListItem>
            <ListItem icon="👾">
              Sharing code in&nbsp;
              <MarkupLink href="https://github.com/mariocesar" />, and projects
              like this website&nbsp;
              <MarkupLink href="https://github.com/mariocesar/mariocesar" />
              <ul role="list">
                <ListItem icon="📝">
                  <span>
                    I have random and sometimes worthy bits of code unordered in{" "}
                    <MarkupLink href="https://gist.github.com/mariocesar" />
                  </span>
                </ListItem>
              </ul>
            </ListItem>
          </ul>
        </div>
      </main>
    </>
  );
}
