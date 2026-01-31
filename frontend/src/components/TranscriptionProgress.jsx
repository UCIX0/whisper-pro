import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, Zap } from 'lucide-react';

export default function TranscriptionProgress({ progress, status, isProcessing }) {
    return (
        <div className="w-full max-w-3xl mx-auto mb-8">
            {/* Status Header */}
            <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                    <div className={`p-1 rounded-full ${isProcessing ? 'animate-pulse text-accent' : 'text-gray-500'}`}>
                        <Cpu size={20} />
                    </div>
                    <span className="text-sm font-medium text-subtext uppercase tracking-wider">
                        {isProcessing ? "Procesando en GPU (CUDA)" : "En Espera"}
                    </span>
                </div>
                <span className="text-white font-mono">{Math.round(progress)}%</span>
            </div>

            {/* Progress Bar Container */}
            <div className="h-4 bg-gray-800 rounded-full overflow-hidden relative shadow-inner">
                {/* Animated Bar */}
                <motion.div
                    className="absolute top-0 left-0 h-full bg-gradient-to-r from-primary via-accent to-primary background-animate"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ type: "spring", stiffness: 50, damping: 15 }}
                    style={{ backgroundSize: "200% 100%" }}
                />

                {/* Shimmer Effect */}
                {isProcessing && (
                    <motion.div
                        className="absolute top-0 left-0 h-full w-full bg-white/20 skew-x-12"
                        initial={{ x: '-100%' }}
                        animate={{ x: '100%' }}
                        transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                    />
                )}
            </div>

            <div className="mt-2 text-xs text-subtext text-right flex justify-end gap-2">
                {status && <span>{status}</span>}
            </div>
        </div>
    );
}
