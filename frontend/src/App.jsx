import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import FileUploader from './components/FileUploader';
import TranscriptionProgress from './components/TranscriptionProgress';
import TranscriptDisplay from './components/TranscriptDisplay';
import { UploadCloud, CheckCircle, Bell } from 'lucide-react';

const API_URL = 'http://localhost:8001';
const WS_URL = 'ws://localhost:8001/ws/transcribe';

// Simple sound synthesizer for a pleasant chime
const playSuccessSound = () => {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;

        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
        osc.frequency.exponentialRampToValueAtTime(1046.5, ctx.currentTime + 0.5); // C6

        gain.gain.setValueAtTime(0.1, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 1.5);

        osc.start();
        osc.stop(ctx.currentTime + 1.5);
    } catch (e) {
        console.error("Audio play failed", e);
    }
};

function App() {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, uploading, processing, complete, error
    const [progress, setProgress] = useState(0);
    const [segments, setSegments] = useState([]);
    const [error, setError] = useState(null);
    const [showSuccessModal, setShowSuccessModal] = useState(false);

    const wsRef = useRef(null);

    // Request notification permission on load
    useEffect(() => {
        if ('Notification' in window && Notification.permission !== 'granted') {
            Notification.requestPermission();
        }
    }, []);

    // Handle completion effects
    useEffect(() => {
        if (status === 'complete') {
            playSuccessSound();
            setShowSuccessModal(true);

            if ('Notification' in window && Notification.permission === 'granted') {
                new Notification('Transcripción Completada', {
                    body: 'Tu archivo ha sido procesado exitosamente.',
                    icon: '/vite.svg' // default vite icon
                });
            }
        }
    }, [status]);

    const handleFileSelected = async (selectedFile) => {
        setFile(selectedFile);
        setStatus('uploading');
        setSegments([]);
        setError(null);
        setProgress(0);
        setShowSuccessModal(false);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error('Falló la subida del archivo');

            const data = await response.json();
            const filePath = data.file_path;

            startTranscription(filePath);
        } catch (err) {
            setError(err.message);
            setStatus('error');
        }
    };

    const startTranscription = (filePath) => {
        setStatus('processing');
        wsRef.current = new WebSocket(WS_URL);

        wsRef.current.onopen = () => {
            wsRef.current.send(JSON.stringify({ file_path: filePath }));
        };

        wsRef.current.onmessage = (event) => {
            const message = JSON.parse(event.data);

            if (message.type === 'progress') {
                // compatibility
            } else if (message.type === 'segment') {
                setSegments(prev => [...prev, message.data]);
                setProgress(message.data.progress);
            } else if (message.type === 'info') {
                console.log("Info:", message.data);
            } else if (message.type === 'complete') {
                setStatus('complete');
                setProgress(100);
                wsRef.current.close();
            } else if (message.type === 'error') {
                setError(message.message);
                setStatus('error');
            }
        };

        wsRef.current.onerror = (e) => {
            setError('Error de conexión WebSocket');
            setStatus('error');
        };
    };

    const handleCopy = () => {
        const text = segments.map(s => s.text).join('\n');
        navigator.clipboard.writeText(text);
    };

    const handleSave = () => {
        const text = segments.map(s => s.text).join('\n');
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${file?.name.split('.')[0] || 'transcript'}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <div className="min-h-screen bg-background text-text flex flex-col items-center p-8 relative overflow-hidden">
            {/* Background Ambient Glow */}
            <div className="absolute top-[-20%] left-[-20%] w-[60%] h-[60%] bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-[-20%] right-[-20%] w-[60%] h-[60%] bg-accent/20 rounded-full blur-[120px] pointer-events-none" />

            {/* Header */}
            <header className="mb-12 text-center z-10 w-full max-w-4xl flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="p-3 bg-gradient-to-br from-primary to-accent rounded-xl shadow-lg shadow-purple-900/50">
                        <UploadCloud size={32} className="text-white" />
                    </div>
                    <h1 className="text-3xl font-bold tracking-tight text-white">
                        Whisper <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-accent">Pro</span>
                    </h1>
                </div>
                <div className="text-xs text-subtext border border-gray-800 rounded-full px-3 py-1 bg-surface/50">
                    Ejecutando en RTX 4070
                </div>
            </header>

            {/* Main Content */}
            <main className="w-full max-w-4xl z-10 flex flex-col gap-8">
                <div className={`${status !== 'idle' && status !== 'error' ? 'hidden' : 'block'}`}>
                    <FileUploader onFileSelected={handleFileSelected} />
                </div>

                <AnimatePresence>
                    {(status === 'processing' || status === 'complete' || status === 'uploading') && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                        >
                            <TranscriptionProgress
                                progress={progress}
                                status={status === 'uploading' ? 'Subiendo...' : status === 'processing' ? 'Transcribiendo...' : 'Completado'}
                                isProcessing={status === 'processing'}
                            />
                        </motion.div>
                    )}
                </AnimatePresence>

                <TranscriptDisplay
                    segments={segments}
                    onCopy={handleCopy}
                    onSave={handleSave}
                    isComplete={status === 'complete'}
                />

                {status === 'error' && (
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="p-4 bg-red-900/30 border border-red-800 text-red-200 rounded-xl text-center"
                    >
                        <p>Error: {error}</p>
                        <button
                            onClick={() => setStatus('idle')}
                            className="mt-2 text-sm underline hover:text-white"
                        >
                            Intentar de nuevo
                        </button>
                    </motion.div>
                )}
            </main>

            {/* Success Modal Overlay */}
            <AnimatePresence>
                {showSuccessModal && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={() => setShowSuccessModal(false)}
                        className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
                    >
                        <motion.div
                            initial={{ scale: 0.5, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.5, opacity: 0 }}
                            className="bg-surface border border-gray-700 p-8 rounded-3xl shadow-2xl text-center max-w-sm mx-4"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <motion.div
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
                                className="w-20 h-20 bg-success/20 rounded-full flex items-center justify-center mx-auto mb-6 text-success"
                            >
                                <CheckCircle size={48} />
                            </motion.div>
                            <h2 className="text-2xl font-bold text-white mb-2">¡Transcripción Lista!</h2>
                            <p className="text-subtext mb-6">Tu archivo ha sido procesado exitosamente.</p>
                            <button
                                onClick={() => setShowSuccessModal(false)}
                                className="bg-white text-black px-6 py-2 rounded-full font-medium hover:bg-gray-200 transition-colors"
                            >
                                Genial
                            </button>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}

export default App;