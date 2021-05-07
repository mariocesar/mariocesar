import Head from 'next/head'
import Page from '@/components/Page'
import { readMarkdownFileConvertToHTML } from '@/lib/markdown'

export async function getStaticProps() {
  const { data, content } = await readMarkdownFileConvertToHTML('README.md')
  return { props: { title: data.Title, content } }
}

export default function Home({ title, content }) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta
          name="google-site-verification"
          content="CPziVTiDUu4mYTO0W7b63PVGE2YKC5lp7Uz-XiIkEWs"
        />
      </Head>
      <Page role="main">
        <article
          className="markdown"
          dangerouslySetInnerHTML={{ __html: content }}
        />
      </Page>
      <script
        dangerouslySetInnerHTML={{ __html: "mixpanel.track('Page viewed')" }}
      />
    </>
  )
}
