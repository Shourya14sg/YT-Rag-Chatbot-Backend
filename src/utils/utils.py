from youtube_transcript_api import FetchedTranscriptSnippet
from models.chunk_model import Chunk
def create_time_based_chunks(snippets:list[FetchedTranscriptSnippet],avg_duration=200,overlap_count=5)->list[Chunk]:
    chunks:list[Chunk]=[]
    current_chunk:list[FetchedTranscriptSnippet] = []
    chunk_start = None
    current_duration = 0
    for s in snippets:
        #combine if they are in duration range
        if chunk_start is None:
            chunk_start=s.start

        current_chunk.append(s)  # ✅ store full snippet
        current_duration += s.duration

        # if threshold reached → finalize chunk
        if current_duration >= avg_duration:
            chunk_text = " ".join(sn.text.strip() for sn in current_chunk)
            chunks.append({
                "start": chunk_start,
                "text": chunk_text
            })
            #overlap N chunks for future chunk
            overlap_snippets = current_chunk[-overlap_count:]
           
            # reset chunk
            current_chunk = overlap_snippets.copy()
            chunk_start = overlap_snippets[0].start
            current_duration = sum(sn.duration for sn in overlap_snippets)

    # ✅ last chunk if it didn't reach the threshold
    if current_chunk:
        chunks.append({
            "start": chunk_start,
            "text": " ".join(sn.text for sn in current_chunk)
        })
    return chunks