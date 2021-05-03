import Head from "next/head";
import Page from "@/components/Page";
import ListItem from "@/components/ListItem";
import MarkupLink from "@/components/MarkupLink";

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
          I'm a software developer, trying to write, create, and mostly being a
          great father. I work at ⚡️<MarkupLink>zapier.com</MarkupLink> as an
          Integration Software Engineer, which I love and relish. I also work in{" "}
          <MarkupLink>humanzilla.com</MarkupLink>, a small boutique two-person
          software agency with my Wife.
        </p>
        <p>I grew up, live and work from Santa Cruz de la Sierra, Bolivia.</p>
        <p>And you’ve found my slice of the internet.</p>
        <p>You can also find me:</p>

        <ul role="list">
          <ListItem icon="🧑🏽‍💻">
            Talking about work in LinkedIn&nbsp;
            <MarkupLink>linkedin.com/in/mariocesar/</MarkupLink>
          </ListItem>

          <ListItem icon="📸">
            Sharing pretty photos at Instagram&nbsp;
            <MarkupLink>instagram.com/mariocesar_bo/</MarkupLink>
          </ListItem>
          <ListItem icon="🎉">
            Speaking in Clubhouse&nbsp;
            <MarkupLink>joinclubhouse.com/@mariocesar</MarkupLink>
            <ul role="list">
              <ListItem icon="☕">
                I host a room in the club "Club del Desayuno" every day at 9 am
                about Accountability and Networking.
                <br />
              </ListItem>
              <ListItem icon="">
                Go to&nbsp;
                <MarkupLink>
                  joinclubhouse.com/club/club-del-desayuno
                </MarkupLink>
                &nbsp;to participate.
              </ListItem>
            </ul>
          </ListItem>
          <ListItem icon="👾">
            Sharing code and projects in&nbsp;
            <MarkupLink>github.com/mariocesar</MarkupLink>, like this
            website&nbsp;
            <MarkupLink>github.com/mariocesar/mariocesar</MarkupLink>
            <ul role="list">
              <ListItem icon="📝">
                I have random and sometimes worthy bits of code unordered in
                &nbsp;
                <MarkupLink>gist.github.com/mariocesar</MarkupLink>
              </ListItem>
            </ul>
          </ListItem>
          <ListItem icon="🐦">
            Saying little in Twitter&nbsp;
            <MarkupLink>twitter.com/mariocesar_bo</MarkupLink>
          </ListItem>
        </ul>
      </Page>
    </>
  );
}
