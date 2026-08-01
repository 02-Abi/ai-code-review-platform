import React, { useState, useEffect } from 'react';

const TypingEffect = ({ strings, typeSpeed = 50, backSpeed = 30, loop = true }) => {
  const [text, setText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const currentString = strings[index];
    let timer;

    if (isDeleting) {
      timer = setTimeout(() => {
        setText(text.slice(0, -1));
        if (text.length === 0) {
          setIsDeleting(false);
          setIndex((prev) => (prev + 1) % strings.length);
        }
      }, backSpeed);
    } else {
      timer = setTimeout(() => {
        setText(currentString.slice(0, text.length + 1));
        if (text.length === currentString.length) {
          if (loop) {
            setTimeout(() => setIsDeleting(true), 1000);
          }
        }
      }, typeSpeed);
    }

    return () => clearTimeout(timer);
  }, [text, isDeleting, index, strings, typeSpeed, backSpeed, loop]);

  return <span>{text}</span>;
};

export default TypingEffect;