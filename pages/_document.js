import Document, { Html, Head, Main, NextScript } from "next/document";

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const initialProps = await Document.getInitialProps(ctx);

    return {
      ...initialProps,
      extraScript: `
        Array.prototype.slice.call(document.querySelectorAll("a[href^=http]")).map((el)=> {
          el.setAttribute("target", "_blank");
          el.setAttribute("title", el.href);
          el.setAttribute("rel", "noopener");
        });
      `,
    };
  }

  render() {
    const { extraScript } = this.props;
    return (
      <Html lang="en">
        <Head itemType="http://schema.org/Blog" itemScope="">
          <link
            rel="shortcut icon"
            type="image/svg+xml"
            href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>👋🏼</text></svg>"
          ></link>
        </Head>
        <body>
          <Main />
          <NextScript />
          <script dangerouslySetInnerHTML={{ __html: extraScript }} />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
