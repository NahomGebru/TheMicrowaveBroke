/* eslint-disable react/prop-types */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable react/jsx-key */
export function Recipes(props) {
<<<<<<< HEAD
	return (
		<li>
			<div>
				<img src={props.recipe_picture} alt="recipe"></img>
			</div>
			<div>
				<b>Recipe: {props.recipe_title} </b>
				<br></br>
				<a href={props.recipe_link}>See Recipe</a>
				<button>Save Recipe</button>
			</div>
		</li>
	);
=======
  return (
    <li>
      <div>
        <img src={props.recipe_picture} alt="recipe"></img>
      </div>
      <div>
        <b>Recipe: {props.recipe_title} </b>
        <br></br>
        <a href={props.recipe_link}>See Recipe</a>
        <button>Save Recipe</button>
      </div>
    </li>
  );
>>>>>>> 297c89307556f44d6f655bb30580b61f67e8778b
}
