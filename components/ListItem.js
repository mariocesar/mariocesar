export default function ListItem({ icon, children }) {
  return (
    <li data-icon={icon}>
      <div>{children}</div>
    </li>
  );
}
