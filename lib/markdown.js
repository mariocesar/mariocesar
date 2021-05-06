import fs from "fs";
import remark from "remark";
import matter from "gray-matter";
import html from "remark-html";

export async function markdownToHTML(content) {
  const result = await remark()
    .use(html, {
      sanitize: false,
      collapseEmptyAttributes: true,
      closeEmptyElements: true,
    })
    .process(content);
  return result.toString();
}

export async function readMarkdownFileConvertToHTML(path) {
  const fileContents = await fs.promises.readFile(path, "utf8");
  const { data, content } = matter(fileContents);
  const result = await markdownToHTML(content);
  return { data, content: result };
}
