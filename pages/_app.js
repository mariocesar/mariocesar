import '@/styles/main.css'

export default function RootLayout({ Component, pageProps }) {
  return (
    <main role="main" className="relative px-4 sm:px-6 lg:px-8">
      <header className="my-12"></header>
      <Component {...pageProps} />
      <footer className="my-12"></footer>
    </main>
  )
}
