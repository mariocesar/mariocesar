import Head from "next/head";
import Page from "../components/Page";

const ListItem = ({ icon, children }) => {
  return (
    <li data-icon={icon}>
      <span>{children}</span>
    </li>
  );
};

const MarkupLink = ({ href }) => {
  let cleanHref = href.startsWith("http") ? href : `https://${href}`;
  return (
    <a target="_blank" href={cleanHref}>
      {href}
    </a>
  );
};

export default function Home() {
  return (
    <>
      <Head>
        <title>Mario-César Señoranis</title>
      </Head>
      <Page role="main">
        <h1>
          👋🏼 Hello,
          <br />
          I’m Mario&minus;César Señoranis
        </h1>
        <p>
          I’m a software developer, trying to write, create, and mostly being a
          great father. I work at ⚡️
          <MarkupLink href="zapier.com" /> as an Integration Software Engineer a
          job that I love. I also spend some time in &nbsp;
          <MarkupLink href="humanzilla.com" /> a two-person software agency with
          my Wife.
        </p>
        <p>I grew up, live and work from Santa Cruz de la Sierra, Bolivia.</p>
        <p>And you’ve found my slice of the internet.</p>
        <p>You can also find me:</p>
        <ul role="list">
          <ListItem icon="🧑🏽‍💻">
            Talking about work in LinkedIn &nbsp;
            <MarkupLink href="linkedin.com/in/mariocesar/" />
          </ListItem>

          <ListItem icon="📸">
            Sharing pretty photos at Instagram &nbsp;
            <MarkupLink href="instagram.com/mariocesar_bo/" />
          </ListItem>
          <ListItem icon="🎉">
            Speaking in Clubhouse &nbsp;
            <MarkupLink href="joinclubhouse.com/@mariocesar" />
            <ul role="list">
              <ListItem icon="☕">
                I host a room in the club "Club del Desayuno" every day at 9 am
                about Accountability and Networking. See &nbsp;
                <MarkupLink href="joinclubhouse.com/club/club-del-desayuno" />
              </ListItem>
            </ul>
          </ListItem>
          <ListItem icon="👾">
            Sharing code in&nbsp;
            <MarkupLink href="github.com/mariocesar" />, and projects like this
            website&nbsp;
            <MarkupLink href="github.com/mariocesar/mariocesar" />
            <ul role="list">
              <ListItem icon="📝">
                <span>
                  I have random and sometimes worthy bits of code unordered in
                  &nbsp;
                  <MarkupLink href="gist.github.com/mariocesar" />
                </span>
              </ListItem>
            </ul>
          </ListItem>
          <ListItem icon="🐦">
            Saying little in Twitter &nbsp;
            <MarkupLink href="twitter.com/mariocesar_bo" />
          </ListItem>
        </ul>
      </Page>
    </>
  );
}
