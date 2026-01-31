import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileAudio, CheckCircle } from 'lucide-react';
import clsx from 'clsx';

export default function FileUploader({ onFileSelected }) {
    const [isDragging, setIsDragging] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDragOver = useCallback((e) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const file = e.dataTransfer.files[0];
            setSelectedFile(file);
            onFileSelected(file);
        }
    }, [onFileSelected]);

    const handleChange = useCallback((e) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setSelectedFile(file);
            onFileSelected(file);
        }
    }, [onFileSelected]);

    return (
        <div className="w-full max-w-2xl mx-auto my-8">
            <motion.div
                layout
                className={clsx(
                    "relative border-2 border-dashed rounded-3xl p-12 text-center transition-all duration-300 cursor-pointer overflow-hidden",
                    isDragging ? "border-accent bg-accent/10 scale-105" : "border-gray-700 bg-surface hover:border-gray-500"
                )}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => document.getElementById('fileInput').click()}
            >
                <input
                    type="file"
                    id="fileInput"
                    className="hidden"
                    onChange={handleChange}
                    accept="audio/*,video/*"
                />

                <AnimatePresence mode="wait">
                    {!selectedFile ? (
                        <motion.div
                            key="prompt"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            className="flex flex-col items-center gap-4"
                        >
                            <div className="p-4 rounded-full bg-gray-800 text-primary">
                                <Upload size={48} />
                            </div>
                            <div>
                                <h3 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent">
                                    Arrastra un archivo de audio
                                </h3>
                                <p className="text-subtext mt-2">o haz clic para buscar</p>
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="selected"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="flex flex-col items-center gap-4"
                        >
                            <motion.div
                                initial={{ rotate: -180 }}
                                animate={{ rotate: 0 }}
                                className="p-4 rounded-full bg-success/20 text-success"
                            >
                                <CheckCircle size={48} />
                            </motion.div>
                            <div>
                                <h3 className="text-xl font-bold text-white mb-1">
                                    Listo para Transcribir
                                </h3>
                                <div className="flex items-center gap-2 text-primary bg-primary/10 px-4 py-1 rounded-full">
                                    <FileAudio size={16} />
                                    <span className="truncate max-w-[200px]">{selectedFile.name}</span>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Decorative background glow */}
                {isDragging && (
                    <motion.div
                        layoutId="glow"
                        className="absolute inset-0 bg-accent/5 z-[-1] blur-xl"
                    />
                )}
            </motion.div>
        </div>
    );
}
