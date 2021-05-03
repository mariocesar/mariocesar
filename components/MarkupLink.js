export default function MarkupLink({ children, title }) {
  let cleanHref = children.startsWith("http")
    ? children.toString().trim()
    : `https://${children.toString().trim()}`;

  return (
    <a target="_blank" title={title || cleanHref} href={cleanHref}>
      {children.toString().trim()}
    </a>
  );
}
