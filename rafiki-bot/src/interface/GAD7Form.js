import { useState } from "react";

const GAD7Form = ({ onSubmit, onClose }) => {
  const questions = [
    "Je, unahisi woga, wasiwasi, au ukingo?",
    "Kutoweza na uwezo wa kuacha au kudhibiti wasiwasi?",
    "Je, una wasiwasi sana kuhusu mambo tofauti?",
    "Shida ya  kupumzika?",
    "Kuwa na wasiwasi sana hivi kwamba ni ngumu kukaa kwa utulivu?",
    "kukasirishwa au kukasirika kwa urahisi?",
    "Kuhisi hofu, kana kwamba kitu kibaya kinaweza kutokea?",
    "ikiwa umekutana na matatizo yoyote yale,je umepata ugumu gani kutokana na matatizo hayo katika ufanyaji wa kazi zako,utuzanji wa vitu nyumbani, au kupatana vizuri na watu wengine?",
  ];

  const options = [
    { label: "chagua jibu", value: "" },
    { label: "sijasumbuliwa kabisa", value: 0 },
    { label: "Siku kadhaa", value: 1 },
    { label: "zaidi ya nusu ya siku zilizotajwa", value: 2 },
    { label: "karibu kila siku", value: 3 },
  ];

  const impactOptions = [
    { label: "chagua jibu", value: "" },
    { label: "sio vigumu kabisa", value: "sio vigumu kabisa" },
    { label: "ugumu kiasi fulani", value: "ugumu kiasi fulani" },
    { label: "vigumu sana", value: "vigumu sana" },
    { label: "vigumu kupita kiasi", value: "vigumu kupita kiasi" },
  ];

  const [responses, setResponses] = useState(Array(10).fill(""));

  const handleResponseChange = (index, value) => {
    const updatedResponses = [...responses];
    updatedResponses[index] = value;
    setResponses(updatedResponses);
  };

 const handleSubmit = (event) => {
  event.preventDefault();

  const totalScore = responses.slice(0, 9).reduce((a, b) => a + (parseInt(b) || 0), 0);
  const impactResponse = responses[9] || "hujachagua jibu yoyote";
  const combinedMessage = `alama ya GAD-7: ${totalScore} | athari kwa maisha ya kila siku: ${impactResponse}`;
  onSubmit(combinedMessage);
  onClose();
};


  return (
    <div className="p-4 bg-white dark:bg-gray-800 dark:text-white rounded-lg shadow-md relative">
      <button onClick={onClose} className="absolute top-2 right-2 text-gray-600 hover:text-red-500">
        ✖
      </button>

      <h2 className="text-lg font-bold mb-2">Fomu ya Tathmini ya GAD-7 ya Wasiwasi</h2>
      <p className= "mb-2">Katika kipindi cha wiki 2 zilizopita, ni mara ngapi  umekuwa ukisumbuliwa na moja ya matatizo yafuatayo?  </p>

      <form onSubmit={handleSubmit}>
        {questions.map((question, index) => (
          <div key={index} className="mb-2">
            <p>{question}</p>
            <select
              className="border p-2 rounded-md w-full dark:bg-gray-800 dark:text-white"
              value={responses[index]}
              onChange={(e) => handleResponseChange(index, e.target.value)}
            >
              {index < 9
                ? options.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))
                : impactOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
            </select>
          </div>
        ))}
        <button type="submit" className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md">
          Submit
        </button>
      </form>
    </div>
  );
};

export default GAD7Form;
