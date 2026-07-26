
from st_aggrid import JsCode

CONFIDENCE_RENDERER = JsCode(
    """
    class ConfidenceRenderer {
        init(params) {
            const rawValue = Number(params.value);
            const value = Number.isFinite(rawValue)
                ? Math.max(0, Math.min(100, rawValue))
                : 0;

            let barColor;

            if (value >= 90) {
                barColor = '#10b981';
            } else if (value >= 60) {
                barColor = '#f59e0b';
            } else {
                barColor = '#ef4444';
            }

            this.eGui = document.createElement('div');

            Object.assign(this.eGui.style, {
                display: 'flex',
                alignItems: 'center',
                width: '100%',
                height: '100%',
                gap: '8px'
            });

            const track = document.createElement('div');

            Object.assign(track.style, {
                flex: '1',
                height: '10px',
                backgroundColor: '#4b5563',
                borderRadius: '999px',
                overflow: 'hidden',
                minWidth: '60px'
            });

            const fill = document.createElement('div');

            Object.assign(fill.style, {
                width: `${value}%`,
                height: '100%',
                backgroundColor: barColor,
                borderRadius: '999px',
                transition: 'width 0.2s ease'
            });

            const label = document.createElement('span');
            label.textContent = `${value.toFixed(0)}%`;

            Object.assign(label.style, {
                minWidth: '38px',
                textAlign: 'right',
                fontSize: '12px',
                fontWeight: '600',
                color: '#f3f4f6'
            });

            track.appendChild(fill);
            this.eGui.appendChild(track);
            this.eGui.appendChild(label);
        }

        getGui() {
            return this.eGui;
        }
    }
    """
)