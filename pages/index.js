import path from 'node:path'
import Head from 'next/head'
import { promises as fs } from 'fs'
import { remark } from 'remark'
import remarkHtml from 'remark-html'
import data from '@/data/person.json'
export default function Home({ readme }) {
  return (
    <>
      <Head>
        <title>Mario−César Señoranis</title>
        <meta
          name="description"
          content="I’m a software developer here is my site and Blog"
        />
        <meta name="author" content="Mario-César Señoranis" />
        <meta
          name="twitter:title"
          content="Mario−César Señoranis | Software Developer"
        />
        <meta
          property="og:title"
          content="Mario−César Señoranis | Software Developer"
        />
        <meta
          property="og:site_name"
          itemProp="name"
          content="Mario−César Señoranis | Software Developer"
        />
        <meta property="og:url" content="https://mariocesar.xyz" />
        <meta property="og:type" content="blog" />
        <meta
          property="og:description"
          content="I’m a software developer here is my site and Blog"
        />
        <meta
          name="twitter:description"
          content="I’m a software developer here is my site and Blog"
        />
        <meta property="article:publisher" content="https://mariocesar.xyz" />
        <meta name="twitter:site" content="@mariocesar_bo" />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
        />
      </Head>
      <article
        className="prose prose-stone mx-auto text-gray-700 prose-h1:tracking-tight lg:prose-h1:leading-snug"
        dangerouslySetInnerHTML={{ __html: readme }}
      />
    </>
  )
}

export async function getStaticProps() {
  const content = await fs.readFile(
    path.join(process.cwd(), 'README.md'),
    'utf8',
  )

  const readme = await remark()
    .use(remarkHtml)
    .process(content)
    .then((file) => file.toString())

  return {
    props: {
      readme,
    },
  }
}
