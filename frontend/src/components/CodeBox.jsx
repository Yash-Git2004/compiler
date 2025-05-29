import { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

export default function CodeBox() {
  const [code, setCode] = useState("");
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [language, setLanguage] = useState("python");

  const navigate = useNavigate();

  const handleRun = async () => {
    setOutput(`Running ${language} code...`);

    try {
      // Step 1: Send POST request
      const postResponse = await fetch("http://localhost:8000/compiler/compile/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language }),
      });

      const postData = await postResponse.json();

      // If no placeholders, directly show output
      if (postData.output) {
        setOutput(postData.output);
      } else if (postData.code_id) {
        // Step 2: Prepare inputs from textarea
        let inputObj = {};
        try {
          // Assume input is a JSON object like: { "input1": "5", "input2": "hello" }
          inputObj = JSON.parse(input);
        } catch (e) {
          setOutput("Invalid input format. Use JSON like {\"input1\": \"5\"}");
          return;
        }

        // Step 3: Send PUT request
        const putResponse = await fetch("http://localhost:8000/compiler/compile/", {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code_id: postData.code_id, inputs: inputObj }),
        });

        const putData = await putResponse.json();
        setOutput(putData.output || "No output returned.");
      } else {
        setOutput("Unexpected server response.");
      }
    } catch (err) {
      console.error(err);
      setOutput("An error occurred while compiling the code.");
    }
  };


  const handleConvert = async () => {
    setOutput("Converting...");
    try {
      const res = await fetch("http://localhost:8001/convert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language, code }),
      });
      const data = await res.json();
      setOutput(data.pseudocode || "No pseudocode generated.");
    } catch (err) {
      setOutput("Error converting code.");
      console.error(err);
    }
  };


  return (
    <div className="min-h-screen bg-[#1e1e1e] text-white">
      {/* Top Nav */}
      <div className="flex justify-between items-center p-4 border-b border-gray-700">
        <motion.h1
          initial={{ x: -200, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 60 }}
          className="text-3xl font-bold text-blue-400"
        >
          CodeBox
        </motion.h1>

        
      </div>

      {/* Main Split Layout */}
      <div className="grid grid-cols-2 gap-4 p-6">
        {/* Left: Code Editor */}
        <div className="flex flex-col space-y-4">
        <select
     value={language}
     onChange={(e) => setLanguage(e.target.value)}
      className="bg-gray-800 p-2 rounded text-white w-fit"
       >
    <option value="python">Python</option>
    <option value="c">C</option>
    
    </select>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="# write your code here..."
            className="h-[400px] p-4 bg-[#2d2d2d] rounded resize-none outline-none"
          />
        </div>

        {/* Right: Input/Output */}
        <div className="flex flex-col space-y-4">
          <div className="flex flex-row space-x-5">
          <button
            onClick={handleRun}
            className="bg-red-500 hover:bg-blue-600 w-fit px-4 py-2 rounded"
          >
            Run
          </button>
          <button
            onClick={handleConvert}
            className="bg-white-500 hover:bg-red-600 w-fit px-4 py-2 rounded"
          >
            Convert
          </button>

          </div>
          
          
          <div className="bg-[#2d2d2d] p-4 rounded h-100 overflow-auto">
            <h2 className="font-semibold mb-2">Output:</h2>
            <pre>{output || "No output yet."}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}
