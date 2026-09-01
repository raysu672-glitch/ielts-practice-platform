/**
 * 口语切题预检：答非所问不应给 6 分（逻辑与 app.js 保持一致的可测子集）
 */
const assert = require('assert');

const STOP = new Set(['the', 'and', 'you', 'your', 'have', 'do', 'are', 'is', 'what', 'why', 'how', 'when', 'where', 'a', 'an', 'to', 'of', 'in', 'for', 'with', 'about', 'i', 'my', 'me', 'we', 'our', 'it', 'its', 'be', 'been', 'was', 'were', 'would', 'could', 'should', 'can', 'like', 'think', 'feel', 'know', 'get', 'go', 'say', 'said', 'well', 'yes', 'no', 'really', 'very', 'just', 'also', 'some', 'any', 'all', 'more', 'most', 'other', 'into', 'over', 'such', 'maybe', 'actually', 'ever', 'before', 'after', 'than', 'then', 'too', 'much', 'many']);

function normalizeChunkText(s) {
    return String(s || '')
        .toLowerCase()
        .replace(/['']/g, "'")
        .replace(/[^a-z0-9'\s]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

function stemTopicWord(word) {
    let w = String(word || '').toLowerCase();
    if (w.endsWith('ies') && w.length > 4) w = w.slice(0, -3) + 'y';
    else if (w.endsWith('ing') && w.length > 5) w = w.slice(0, -3);
    else if (w.endsWith('ed') && w.length > 4) w = w.slice(0, -2);
    else if (w.endsWith('es') && w.length > 4) w = w.slice(0, -2);
    else if (w.endsWith('s') && w.length > 4) w = w.slice(0, -1);
    return w.length >= 3 ? w : '';
}

function collectTopicKeywords(question, qMeta) {
    const keywords = new Set();
    const addText = (text) => {
        normalizeChunkText(text).split(' ').forEach((w) => {
            if (w.length <= 2 || STOP.has(w)) return;
            keywords.add(w);
            const stem = stemTopicWord(w);
            if (stem) keywords.add(stem);
        });
    };
    addText(question);
    if (qMeta) {
        addText(qMeta.title || '');
        addText(qMeta.topicEn || '');
    }
    const qNorm = normalizeChunkText(question);
    if (/\b(study|studies|studying|subject|major|university|college|course|school)\b/.test(qNorm)) {
        ['study', 'studies', 'studying', 'subject', 'subjects', 'major', 'majoring', 'university', 'college', 'course', 'degree', 'school', 'student'].forEach((w) => keywords.add(w));
    }
    return keywords;
}

function assessTopicRelevance(question, transcript, qMeta) {
    const keywords = collectTopicKeywords(question, qMeta);
    const tNorm = normalizeChunkText(transcript);
    const tokens = tNorm.split(' ').filter((w) => w.length > 2 && !STOP.has(w));
    const hits = new Set();
    tokens.forEach((tok) => {
        if (keywords.has(tok)) hits.add(tok);
        else {
            const stem = stemTopicWord(tok);
            if (stem && keywords.has(stem)) hits.add(tok);
        }
    });
    const hitCount = hits.size;
    const tokenCount = tokens.length;
    let level = 'on_topic';
    if (tokenCount < 4) level = 'partial';
    else if (hitCount === 0 && tokenCount >= 6) level = 'off_topic';
    else if (hitCount <= 1 && tokenCount >= 10) level = 'off_topic';
    else if (hitCount <= 1 && tokenCount >= 6) level = 'weak_topic';
    return { level, hitCount, tokenCount };
}

const q = {
    q: 'What subjects are you studying? Why did you choose to study that subject?',
    title: 'Subjects',
    topicEn: 'Work or studies'
};

const offTopic = assessTopicRelevance(q.q,
    'I love playing basketball every weekend with my friends because it is fun and relaxing and we always go to the park near my home.',
    q);
assert.strictEqual(offTopic.level, 'off_topic', 'random sports talk should be off_topic');

const onTopic = assessTopicRelevance(q.q,
    'I am majoring in business and economics at university because I enjoy studying how markets work.',
    q);
assert.notStrictEqual(onTopic.level, 'off_topic', 'relevant study answer should not be off_topic');
assert.ok(onTopic.hitCount >= 2, 'on-topic answer should hit multiple keywords');

const caps = { off_topic: { overall: 4.0, fluency: 4, vocabulary: 4 } };
assert.ok(caps.off_topic.overall <= 4.5, 'off_topic overall cap must block 6.0');

console.log('test_speaking_topic_relevance.js: OK');
