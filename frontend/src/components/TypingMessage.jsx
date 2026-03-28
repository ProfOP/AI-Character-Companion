import { useEffect, useState } from "react";

export default function TypingMessage({ text, speed = 12, onDone }) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    let i = 0;
    setDisplayed("");

    const interval = setInterval(() => {
      i++;
      setDisplayed(text.slice(0, i));

      if (i >= text.length) {
        clearInterval(interval);
        onDone && onDone();
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text]);

  return <span>{displayed}</span>;
}