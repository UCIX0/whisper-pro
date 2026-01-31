import React, { useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Copy, Download, Check } from 'lucide-react';

export default function TranscriptDisplay({ segments, onCopy, onSave, isComplete }) {
    const containerRef = useRef(null);
    const [copied, setCopied] = React.useState(false);

    // Auto-scroll to bottom
    useEffect(() => {
        if (containerRef.current) {
            containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
    }, [segments]);

    const handleCopy = () => {
        onCopy();
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (segments.length === 0) return null;

    return (
        <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="w-full max-w-4xl mx-auto bg-surface/50 backdrop-blur-md rounded-2xl border border-gray-800 overflow-hidden shadow-2xl"
        >
            {/* Header / Toolbar */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-800 bg-black/20">
                <h2 className="text-lg font-semibold text-white">Transcripción</h2>
                <div className="flex gap-2">
                    <button
                        onClick={handleCopy}
                        className="p-2 hover:bg-white/10 rounded-lg text-subtext hover:text-white transition-colors flex items-center gap-2"
                        title="Copiar al Portapapeles"
                    >
                        {copied ? <Check size={18} className="text-success" /> : <Copy size={18} />}
                        <span className="text-xs">{copied ? '¡Copiado!' : 'Copiar'}</span>
                    </button>
                    <button
                        onClick={onSave}
                        disabled={!isComplete}
                        className={`p-2 rounded-lg transition-colors flex items-center gap-2 ${isComplete ? 'hover:bg-white/10 text-subtext hover:text-white cursor-pointer' : 'opacity-50 cursor-not-allowed text-gray-600'
                            }`}
                        title="Guardar como TXT"
                    >
                        <Download size={18} />
                        <span className="text-xs">Guardar</span>
                    </button>
                </div>
            </div>

            {/* Text Area */}
            <div
                ref={containerRef}
                className="p-6 max-h-[60vh] overflow-y-auto scroll-smooth font-serif text-lg leading-relaxed text-gray-200"
            >
                <AnimatePresence>
                    {segments.map((segment, index) => (
                        <motion.p
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, ease: "easeOut" }}
                            className="mb-4"
                        >
                            <span className="text-xs text-gray-600 font-sans mr-2 select-none">
                                [{new Date(segment.start * 1000).toISOString().substr(14, 5)}]
                            </span>
                            {segment.text}
                        </motion.p>
                    ))}
                </AnimatePresence>
                {/* Blinking cursor effect at the end if not complete */}
                {!isComplete && (
                    <span className="inline-block w-2 h-5 bg-accent ml-1 align-middle animate-pulse" />
                )}
            </div>
        </motion.div>
    );
}
