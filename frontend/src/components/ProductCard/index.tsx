import { Link } from "react-router";
import { Card } from "../../types/cardType";
import styles from "./index.module.scss";

const ProductCard = (props: Card) => {
  return (
    <Link to={`/card/${props.id}`} key={props.id} className={styles.card}>
      <img
        className={styles.card__img}
        src={props.destination.image}
        alt={`photo_${props.id}`}
      />
      <p className={styles.card__title}>
        Название:{" "}
        {props.name.length > 15 ? props.name.slice(0, 15) + "..." : props.name}
      </p>
      <p className={styles.card__title}>
        Описание:{" "}
        {props.description.length > 15
          ? props.description.slice(0, 15) + "..."
          : props.description}
      </p>
      <p className={styles.card__price}>Цена: {props.price} ₽</p>
    </Link>
  );
};

export default ProductCard;
