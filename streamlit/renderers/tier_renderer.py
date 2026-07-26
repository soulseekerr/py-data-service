
from st_aggrid import JsCode

TIER_RENDERER = JsCode(
    """
    class TierRenderer {
        init(params) {
            const tierNumber = Number(
                String(params.value).replace(/[^0-9]/g, '')
            );

            const styles = {
                1: { background: '#dbeafe', color: '#1e3a8a' },
                2: { background: '#dcfce7', color: '#14532d' },
                3: { background: '#fef3c7', color: '#78350f' },
                4: { background: '#fed7aa', color: '#7c2d12' },
                5: { background: '#f3e8ff', color: '#581c87' },
                6: { background: '#fee2e2', color: '#7f1d1d' }
            };

            const style = styles[tierNumber] || {
                background: '#e5e7eb',
                color: '#111827'
            };

            this.eGui = document.createElement('span');
            this.eGui.textContent = params.value ?? '';

            Object.assign(this.eGui.style, {
                display: 'inline-flex',
                justifyContent: 'center',
                minWidth: '60px',
                padding: '2px 8px',
                borderRadius: '6px',
                fontWeight: '600',
                backgroundColor: style.background,
                color: style.color
            });
        }

        getGui() {
            return this.eGui;
        }
    }
    """
)