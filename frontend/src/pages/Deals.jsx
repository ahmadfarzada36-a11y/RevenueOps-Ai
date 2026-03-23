import Layout from "../layout/DashboardLayout";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import { useEffect, useState } from "react";
import { getDeals, updateDealStatus } from "../services/dealService";

const cols = ["lead", "contacted", "won", "lost"];

export default function Deals() {
  const [deals, setDeals] = useState([]);

  useEffect(() => {
    getDeals().then(res => setDeals(res.data));
  }, []);

  const onDragEnd = (res) => {
    if (!res.destination) return;

    const id = res.draggableId;
    const status = res.destination.droppableId;

    updateDealStatus(id, status);

    setDeals(prev =>
      prev.map(d => d.id == id ? { ...d, status } : d)
    );
  };

  return (
    <Layout>
      <DragDropContext onDragEnd={onDragEnd}>
        <div className="grid grid-cols-4 gap-4">

          {cols.map(c => (
            <Droppable droppableId={c} key={c}>
              {(p) => (
                <div ref={p.innerRef} {...p.droppableProps}
                  className="bg-gray-100 p-4 min-h-[400px]">

                  {deals.filter(d => d.status === c).map((d, i) => (
                    <Draggable key={d.id} draggableId={String(d.id)} index={i}>
                      {(p) => (
                        <div ref={p.innerRef} {...p.draggableProps} {...p.dragHandleProps}
                          className="bg-white p-2 mb-2">
                          {d.name}
                        </div>
                      )}
                    </Draggable>
                  ))}

                  {p.placeholder}
                </div>
              )}
            </Droppable>
          ))}

        </div>
      </DragDropContext>
    </Layout>
  );
}
