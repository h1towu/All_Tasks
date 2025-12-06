// ==UserScript==
// @name        VALORANT Visual Helper (Client-Side)
// @namespace   local
// @version     1.0
// @description Безопасный анализ изображения через браузер
// @match       https://playvalorant.com/*
// @grant       none
// ==/UserScript==

(function() {
    'use strict';

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const video = document.createElement('video');
    let stream;

    // Захват экрана через браузер (требует разрешение пользователя)
    async function startCapture() {
        try {
            stream = await navigator.mediaDevices.getDisplayMedia({
                video: { displaySurface: "monitor" },
                audio: false
            });
            video.srcObject = stream;
            video.play();
            requestAnimationFrame(analyzeFrame);
        } catch (err) {
            console.log("Ошибка захвата экрана:", err);
        }
    }

    // Анализ кадра (поиск цветов, характерных для моделей)
    function analyzeFrame() {
        if (video.readyState !== video.HAVE_ENOUGH_DATA) return;

        // Устанавливаем размер canvas под размер видео
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Рисуем кадр видео на canvas
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        // Простой поиск по цвету (например, красные вражеские модели)
        for (let i = 0; i < data.length; i += 4) {
            const red = data[i];
            const green = data[i + 1];
            const blue = data[i + 2];

            // Пример: поиск красных оттенков (враги в VALORANT часто выделены красным)
            if (red > 150 && green < 50 && blue < 50) {
                // Можно добавить маркеры, но для минимального риска просто логируем
                data[i + 1] = 255; // Делаем пиксель зеленым (визуальная помощь)
            }
        }

        ctx.putImageData(imageData, 0, 0);
        requestAnimationFrame(analyzeFrame);
    }

    // Overlay поверх игры
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '999999';
    canvas.style.pointerEvents = 'none';
    document.body.appendChild(canvas);

    // Запуск только при явном действии пользователя (без автоматизации)
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.code === 'KeyH') {
            startCapture();
        }
    });

    console.log('Безопасный помощник активирован. Нажмите Alt+H для запуска.');
})();