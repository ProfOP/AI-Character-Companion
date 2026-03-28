export default function MessageRenderer({ text }) {
    if (!text) return null;
  
    const blocks = text.split("\n").filter((b) => b.trim() !== "");
  
    return (
      <div className="space-y-3">
        {blocks.map((block, i) => {
          const isNarration =
            block.startsWith("*") && block.endsWith("*");
  
          if (isNarration) {
            return (
              <p
                key={i}
                className="italic text-gray-400 leading-relaxed"
              >
                {block.slice(1, -1)}
              </p>
            );
          }
  
          return (
            <p key={i} className="text-white leading-relaxed">
              {block}
            </p>
          );
        })}
      </div>
    );
  }