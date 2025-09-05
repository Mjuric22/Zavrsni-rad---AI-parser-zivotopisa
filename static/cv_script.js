// CV Parser JavaScript

class CVParserApp {
    constructor() {
        this.selectedFile = null;
        this.processingResults = null;
        this.initializeApp();
    }

    initializeApp() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File input change
        document.getElementById('fileInput').addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });

        // Drag and drop events
        const uploadArea = document.getElementById('fileUploadArea');
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });

        // Click on upload area to trigger file input
        uploadArea.addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });
    }

    handleFileSelect(file) {
        if (!file) return;

        // Validate file type
        const allowedTypes = [
            '.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'
        ];
        
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExtension)) {
            this.showError(`Nepodržan tip datoteke: ${fileExtension}`);
            return;
        }

        // Validate file size (50MB limit)
        const maxSize = 50 * 1024 * 1024; // 50MB
        if (file.size > maxSize) {
            this.showError('Datoteka je prevelika. Maksimalna veličina je 50MB.');
            return;
        }

        this.selectedFile = file;
        this.displayFileInfo(file);
        this.enableProcessButton();
    }

    displayFileInfo(file) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const uploadArea = document.getElementById('fileUploadArea');

        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        fileInfo.style.display = 'flex';
        
        // Hide the drag and drop area when file is selected
        uploadArea.style.display = 'none';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    removeFile() {
        this.selectedFile = null;
        const fileInfo = document.getElementById('fileInfo');
        const uploadArea = document.getElementById('fileUploadArea');
        
        fileInfo.style.display = 'none';
        // Show the drag and drop area again when file is removed
        uploadArea.style.display = 'block';
        
        document.getElementById('fileInput').value = '';
        this.disableProcessButton();
        this.hideResults();
    }

    enableProcessButton() {
        const processBtn = document.getElementById('processBtn');
        processBtn.disabled = false;
    }

    disableProcessButton() {
        const processBtn = document.getElementById('processBtn');
        processBtn.disabled = true;
    }

    async processCV() {
        if (!this.selectedFile) {
            this.showError('Molimo odaberite datoteku prvo.');
            return;
        }

        this.showLoading();
        this.hideResults();

        try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);
            
            // Add position type
            const positionType = document.getElementById('positionType').value;
            formData.append('position_type', positionType);

            const response = await fetch('/api/upload-cv', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.displayResults(result);
            } else {
                const errorMessage = result.error || 'Obrađa CV-a neuspješna';
                this.showError(errorMessage);
            }
        } catch (error) {
            console.error('Greška pri obradi CV-a:', error);
            this.showError('Mrežna greška. Molimo pokušajte ponovo.');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(result) {
        this.processingResults = result;
        
        // Display processed markdown
        this.updateProcessedContent(result.processed_markdown);
        
        // Display raw data
        this.updateRawContent(result.raw_data);
        
        // Display original text
        this.updateOriginalContent(result.text);
        
        // Show results section
        document.getElementById('resultsSection').style.display = 'block';
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    updateProcessedContent(markdown) {
        const processedContent = document.getElementById('processedContent');
        
        // Convert markdown to HTML (simple conversion)
        const html = this.markdownToHtml(markdown);
        processedContent.innerHTML = html;
    }

    updateRawContent(rawData) {
        const rawContent = document.getElementById('rawContent');
        rawContent.textContent = JSON.stringify(rawData, null, 2);
    }

    updateOriginalContent(text) {
        const originalContent = document.getElementById('originalContent');
        originalContent.textContent = text;
    }

    markdownToHtml(markdown) {
        // Simple markdown to HTML conversion
        return markdown
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*)\*/gim, '<em>$1</em>')
            .replace(/^- (.*$)/gim, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            .replace(/^(?!<[h|u|l])/gm, '<p>')
            .replace(/(?<!>)$/gm, '</p>');
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');
    }

    showLoading() {
        const processBtn = document.getElementById('processBtn');
        const btnText = processBtn.querySelector('.btn-text');
        const spinner = processBtn.querySelector('.spinner');
        
        btnText.textContent = 'Obrađujem...';
        spinner.style.display = 'block';
        processBtn.disabled = true;
        
        document.getElementById('loadingSection').style.display = 'block';
    }

    hideLoading() {
        const processBtn = document.getElementById('processBtn');
        const btnText = processBtn.querySelector('.btn-text');
        const spinner = processBtn.querySelector('.spinner');
        
        btnText.textContent = 'Obrađi CV';
        spinner.style.display = 'none';
        processBtn.disabled = false;
        
        document.getElementById('loadingSection').style.display = 'none';
    }

    showError(message) {
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorSection.style.display = 'none';
        }, 5000);
    }

    hideResults() {
        document.getElementById('resultsSection').style.display = 'none';
    }

    downloadMarkdown() {
        if (this.processingResults) {
            const content = this.processingResults.processed_markdown;
            const fileName = this.selectedFile.name.split('.')[0] + '_processed.md';
            this.downloadFile(content, fileName, 'text/markdown');
        }
    }

    downloadHTML() {
        if (this.processingResults) {
            const markdown = this.processingResults.processed_markdown;
            const html = this.markdownToHtml(markdown);
            const fullHtml = `
<!DOCTYPE html>
<html lang="hr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV Profil</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; line-height: 1.6; }
        h1 { color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 0.5rem; }
        h2 { color: #374151; margin-top: 2rem; }
        h3 { color: #6b7280; }
        ul { margin: 1rem 0; }
        li { margin-bottom: 0.5rem; }
        strong { color: #1f2937; }
    </style>
</head>
<body>
    ${html}
</body>
</html>`;
            const fileName = this.selectedFile.name.split('.')[0] + '_profile.html';
            this.downloadFile(fullHtml, fileName, 'text/html');
        }
    }

    copyToClipboard() {
        if (this.processingResults) {
            const content = this.processingResults.processed_markdown;
            navigator.clipboard.writeText(content).then(() => {
                this.showNotification('Kopirano u međuspremnik!', 'success');
            }).catch(() => {
                this.showNotification('Greška pri kopiranju', 'error');
            });
        }
    }

    downloadFile(content, fileName, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#2563eb'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            font-weight: 500;
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 3000);
    }
}

// Global functions for HTML onclick handlers
function removeFile() {
    if (window.cvParserApp) {
        window.cvParserApp.removeFile();
    }
}

function processCV() {
    if (window.cvParserApp) {
        window.cvParserApp.processCV();
    }
}

function downloadMarkdown() {
    if (window.cvParserApp) {
        window.cvParserApp.downloadMarkdown();
    }
}

function downloadHTML() {
    if (window.cvParserApp) {
        window.cvParserApp.downloadHTML();
    }
}

function copyToClipboard() {
    if (window.cvParserApp) {
        window.cvParserApp.copyToClipboard();
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cvParserApp = new CVParserApp();
});
