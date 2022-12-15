export function calcFontSize(word, allWords, theBiggestWordValue, theSmallestWordValue) {
    const maxSize = 100;
    const minSize = 10;

    let size = ((word.value - theSmallestWordValue) / theBiggestWordValue) * maxSize;
    let firstQuater = (theBiggestWordValue - theSmallestWordValue) / 4;

    if(word.value < firstQuater) {
        let computedSize = size + Math.log10(word.value) * 4;
        return computedSize;
    }

    return size;
}

export function calcPadding (allWords) {
    return 10;
}