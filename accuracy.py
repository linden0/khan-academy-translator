from sentence_transformers import SentenceTransformer, util
from bert_score import score
from statistics import mean


def bert_score_accuracy(text1,text2):
    P, R, F1 = score(text1, text2, lang='en', verbose=True)

    mean_F1 = round(F1.mean().item(),3)
    P = [round(i,3) for i in P.tolist()]
    R = [round(i,3) for i in R.tolist()]
    F1 = [round(i,3) for i in F1.tolist()]
    return mean_F1, P, R, F1


def sbert_accuracy(text1,text2):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Compute embedding for both lists
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)

    # Compute cosine-similarits
    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    scores = []
    # Output the pairs with their score
    for i in range(len(text1)):
        # print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[i], cosine_scores[i][i]))
        scores.append(cosine_scores[i][i].item())
    return (round(mean(scores), 3), [round(i, 3) for i in scores])
