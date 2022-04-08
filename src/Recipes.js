/* eslint-disable react/prop-types */
/* eslint-disable react/react-in-jsx-scope */
/* eslint-disable react/jsx-key */
export function Recipes(props) {
	return (
		<li>
			<div style="float: left">
				<img src={props.recipe_picture} alt="recipe"></img>
			</div>
			<div>
				<b>Recipe: {props.recipe_title} </b>
				<br></br>
				<a href={props.recipe_link}>See Recipe</a>
				{/* <button onClick={props.saveRecipe}>Save Recipe</button> */}
			</div>
		</li>
	);
}
