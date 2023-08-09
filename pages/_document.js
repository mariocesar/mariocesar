import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en" className="h-full bg-white lg:bg-gray-50">
      <Head>
        <meta name="robots" content="follow, index" />
        <meta content="#ffffff" name="theme-color" />
        <meta content="#ffffff" name="msapplication-TileColor" />
        <meta
          name="google-site-verification"
          content="CPziVTiDUu4mYTO0W7b63PVGE2YKC5lp7Uz-XiIkEWs"
        />
      </Head>
      <body className="flex min-h-full flex-col font-sans text-gray-600 antialiased">
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
