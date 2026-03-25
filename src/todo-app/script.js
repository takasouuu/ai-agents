const STORAGE_KEY = "todo-app-items";

const form = document.getElementById("todo-form");
const input = document.getElementById("todo-input");
const dueInput = document.getElementById("due-input");
const list = document.getElementById("todo-list");
const emptyMessage = document.getElementById("empty-message");
const clearCompletedButton = document.getElementById("clear-completed");
const filterButtons = document.querySelectorAll(".filter-btn");

let todos = loadTodos();
let currentFilter = "all"; // "all" | "active" | "completed"

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    currentFilter = btn.dataset.filter;
    filterButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    render();
  });
});

render();

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const text = input.value.trim();
  if (!text) {
    return;
  }

  const dueDate = dueInput.value || null;

  todos.unshift({
    id: crypto.randomUUID(),
    text,
    completed: false,
    dueDate,
  });

  saveTodos();
  render();
  form.reset();
  input.focus();
});

clearCompletedButton.addEventListener("click", () => {
  todos = todos.filter((todo) => !todo.completed);
  saveTodos();
  render();
});

list.addEventListener("click", (event) => {
  const target = event.target;

  if (!(target instanceof HTMLElement)) {
    return;
  }

  const item = target.closest("li");
  if (!item) {
    return;
  }

  const id = item.dataset.id;
  if (!id) {
    return;
  }

  if (target.classList.contains("delete-btn")) {
    todos = todos.filter((todo) => todo.id !== id);
    saveTodos();
    render();
    return;
  }

  if (target.classList.contains("todo-check")) {
    todos = todos.map((todo) =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );
    saveTodos();
    render();
  }
});

function render() {
  list.innerHTML = "";

  const filtered = todos.filter((todo) => {
    if (currentFilter === "active") return !todo.completed;
    if (currentFilter === "completed") return todo.completed;
    return true;
  });

  const todayStr = new Date().toISOString().slice(0, 10);

  filtered.forEach((todo) => {
    const li = document.createElement("li");
    li.className = "todo-item";
    li.dataset.id = todo.id;

    const left = document.createElement("div");
    left.className = "todo-left";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "todo-check";
    checkbox.checked = todo.completed;

    const text = document.createElement("span");
    text.className = `todo-text${todo.completed ? " completed" : ""}`;
    text.textContent = todo.text;

    left.append(checkbox, text);

    if (todo.dueDate) {
      const badge = document.createElement("span");
      badge.className = "due-badge";
      if (!todo.completed) {
        if (todo.dueDate < todayStr) badge.classList.add("overdue");
        else if (todo.dueDate === todayStr) badge.classList.add("today");
      }
      badge.textContent = formatDate(todo.dueDate);
      left.append(badge);
    }

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "delete-btn";
    deleteButton.textContent = "削除";

    li.append(left, deleteButton);
    list.append(li);
  });

  emptyMessage.hidden = filtered.length > 0;
}

function formatDate(dateStr) {
  const [y, m, d] = dateStr.split("-");
  return `${y}/${m}/${d}`;
}

function loadTodos() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return [];
    }

    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed.filter(
      (item) =>
        item &&
        typeof item.id === "string" &&
        typeof item.text === "string" &&
        typeof item.completed === "boolean"
    ).map((item) => ({ ...item, dueDate: item.dueDate ?? null }));
  } catch {
    return [];
  }
}

function saveTodos() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}
