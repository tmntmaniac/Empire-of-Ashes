import { AlertTriangle } from "lucide-react";

export default function ConfirmDialog({
    open,
    title = "Confirm",
    eyebrow = "// Confirm Action",
    message,
    confirmLabel = "Confirm",
    cancelLabel = "Cancel",
    onConfirm,
    onCancel,
    destructive = false,
    testId = "confirm-dialog",
}) {
    if (!open) return null;

    const accent = destructive ? "#C2392E" : "#C2A165";

    return (
        <div
            className="fixed inset-0 z-[60] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
            data-testid={testId}
            onClick={onCancel}
        >
            <div
                className="panel corner-frame w-full max-w-md bg-[#0A0C0B] p-6"
                onClick={(e) => e.stopPropagation()}
            >
                <div
                    className="font-mono text-[11px] tracking-[0.4em] uppercase mb-2"
                    style={{ color: accent }}
                >
                    {eyebrow}
                </div>
                <div className="flex items-start gap-3 mb-4">
                    {destructive && (
                        <AlertTriangle className="w-6 h-6 mt-1 flex-shrink-0" style={{ color: accent }} strokeWidth={2} />
                    )}
                    <div>
                        <h2 className="font-display text-3xl uppercase tracking-tight mb-2 text-[#E0E0E0]">{title}</h2>
                        {message && <p className="text-sm text-[#B8B8B8] font-sans leading-relaxed">{message}</p>}
                    </div>
                </div>

                <div className="flex gap-2 justify-end pt-4 border-t border-[#222]">
                    <button
                        type="button"
                        onClick={onCancel}
                        className="btn-ghost"
                        data-testid={`${testId}-cancel`}
                        autoFocus
                    >
                        {cancelLabel}
                    </button>
                    <button
                        type="button"
                        onClick={onConfirm}
                        className={destructive ? "btn-danger" : "btn-primary"}
                        data-testid={`${testId}-confirm`}
                    >
                        {confirmLabel}
                    </button>
                </div>
            </div>
        </div>
    );
}
