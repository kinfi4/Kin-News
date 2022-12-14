export function calcFontSize(word, wordsCount) {
    let wordsCountCoef = 1 / (wordsCount / 100);
    return Math.log2(word.value) * 30;
}

export function calcPadding (wordsCount) {
    if (wordsCount > 200) {
        return 5;
    } else if (wordsCount > 100) {
        return 10;
    }

    return 20;
}