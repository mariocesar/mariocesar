export default function MarkupLink({ children, title }) {
  let cleanHref = children.startsWith("http")
    ? children.toString().trim()
    : `https://${children.toString().trim()}`;

  return (
    <a
      target="_blank"
      rel="noopener"
      tabindex="0"
      title={title || cleanHref}
      href={cleanHref}
    >
      {children.toString().trim()}
    </a>
  );
}
