import { artifactUrl } from "../services/api";

export default function DownloadButton({ url, children }) {
  if (!url) return null;
  return <a className="secondary button-link" href={artifactUrl(url)}>{children}</a>;
}

