
from st_aggrid import JsCode

STATUS_BADGE_RENDERER = JsCode(
    """
    class StatusBadgeRenderer {
        init(params) {
            const styles = {
                OK: {
                    background: '#d1fae5',
                    colour: '#065f46',
                    border: '#34d399'
                },
                Changed: {
                    background: '#fef3c7',
                    colour: '#78350f',
                    border: '#fbbf24'
                },
                Review: {
                    background: '#fed7aa',
                    colour: '#7c2d12',
                    border: '#fb923c'
                },
                Error: {
                    background: '#fee2e2',
                    colour: '#7f1d1d',
                    border: '#f87171'
                }
            };

            const value = params.value ?? '';
            const style = styles[value] || {
                background: '#e5e7eb',
                colour: '#111827',
                border: '#9ca3af'
            };

            this.eGui = document.createElement('span');
            this.eGui.innerText = value;

            Object.assign(this.eGui.style, {
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '2px 10px',
                borderRadius: '999px',
                fontSize: '12px',
                fontWeight: '600',
                lineHeight: '20px',
                backgroundColor: style.background,
                color: style.colour,
                border: `1px solid ${style.border}`
            });
        }

        getGui() {
            return this.eGui;
        }
    }
    """
)