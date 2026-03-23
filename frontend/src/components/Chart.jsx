import { useEffect, useRef } from "react";
import Chart from "chart.js/auto";

export default function ChartComponent() {
  const ref = useRef();

  useEffect(() => {
    new Chart(ref.current, {
      type: "bar",
      data: {
        labels: ["Won", "Lost"],
        datasets: [{ data: [12, 5] }]
      }
    });
  }, []);

  return <canvas ref={ref}></canvas>;
}
