// Une file d'attente typée
interface Job<T> {
  id: number;
  payload: T;
  done?: boolean;
}

export class Queue<T> {
  private items: Job<T>[] = [];
  push(payload: T): number {
    const id = this.items.length + 1;
    this.items.push({ id, payload, done: false });
    return id;
  }
}
