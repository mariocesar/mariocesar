import fs from 'fs'
import remark from 'remark'
import matter from 'gray-matter'
import html from 'remark-html'
import visit from 'unist-util-visit'
import { normalizeConfig } from 'next/dist/next-server/server/config-shared'

export async function markdownToHTML(content) {
  const result = await remark()
    .use(updateLink)
    .use(html, {
      sanitize: false,
      collapseEmptyAttributes: true,
      closeEmptyElements: true,
    })
    .process(content)
  return result.toString()
}

export async function readMarkdownFileConvertToHTML(path) {
  const fileContents = await fs.promises.readFile(path, 'utf8')
  const { data, content } = matter(fileContents)
  const result = await markdownToHTML(content)
  return { data, content: result }
}

function updateLink() {
  return (ast) => {
    return visit(ast, 'link', (node, index, parent) => {
      const { url } = node
      if (url.startsWith('http')) {
        node.title = url
        node.data = {
          hProperties: {
            target: '_blank',
            rel: 'noopener',
          },
        }
      }
    })
  }
}
