import "./App.css";
import { useState, useEffect } from "react";
// import { Review } from "./Review.js";

function App() {
	// const [val, setVal] = useState([]);
	const [ingredientList, setIngredientList] = useState([{ ingredient: "" }]);
	const [getRecipe, setGetRecipe] = useState(false);

	// function handleDelete(i) {
	// 	setVal([...val.slice(0, i), ...val.slice(i + 1)]);
	// }

	// function handleRatingChange(i, e) {
	// 	const newReviews = val.slice();
	// 	newReviews[i].rating = e.target.value;
	// 	setVal(newReviews);
	// }

	// function handleCommentChange(i, e) {
	// 	const newReviews = val.slice();
	// 	newReviews[i].comment = e.target.value;
	// 	setVal(newReviews);
	// }

	let handleChange = (i, e) => {
		let newFormValues = [...ingredientList];
		newFormValues[i][e.target.ingredient] = e.target.value;
		setIngredientList(newFormValues);
	};

	let addFormFields = () => {
		setIngredientList([...ingredientList, { ingredient: "" }]);
	};

	let removeFormFields = (i) => {
		let newFormValues = [...ingredientList];
		newFormValues.splice(i, 1);
		setIngredientList(newFormValues);
	};

	let handleSubmit = (event) => {
		event.preventDefault();
		alert(JSON.stringify(ingredientList));
	};

	// function onClickSave() {
	// 	fetch("/save_reviews", {
	// 		method: "POST",
	// 		headers: {
	// 			"Content-Type": "application/json",
	// 		},
	// 		body: JSON.stringify(val),
	// 	})
	// 		.then((response) => response.json())
	// 		.then((data) => {
	// 			console.log(data);
	// 		});
	// }

	// const reviews = val.map((review, i) => (
	// 	<Review
	// 		movieID={review.movie_id}
	// 		rating={review.rating}
	// 		comment={review.comment}
	// 		onDelete={() => handleDelete(i)}
	// 		onEdit={(e) => handleCommentChange(i, e)}
	// 		onRate={(e) => handleRatingChange(i, e)}
	// 	/>
	// ));

	// useEffect(() => {
	// 	fetch("/get_reviews", {
	// 		method: "GET",
	// 		headers: {
	// 			"Content-Type": "application/json",
	// 		},
	// 	})
	// 		.then((response) => response.json())
	// 		.then((data) => {
	// 			setVal(data);
	// 		});
	// }, []);

	if (getRecipe == false) {
		return (
			<div>
				<a href="/logout">Log out</a>
				<h1>Recipe Generator</h1>
				<p>Please enter your list of ingredients!</p>
				<form onSubmit={handleSubmit}>
					{ingredientList.map((element, index) => (
						<div className="form-inline" key={index}>
							<label>{index + 1}.</label>
							<input
								type="text"
								name="ingredient"
								value={element.ingredient || ""}
								onChange={(e) => handleChange(index, e)}
							/>
							{index ? (
								<button
									type="button"
									className="button remove"
									onClick={() => removeFormFields(index)}
								>
									Remove
								</button>
							) : null}
						</div>
					))}
					<div>
						<button
							className="button add"
							type="button"
							onClick={() => addFormFields()}
						>
							Add
						</button>
						<button className="button submit" type="submit">
							Submit
						</button>
					</div>
				</form>
			</div>
		);
	} else {
		return (
			<div className="App">
				<h1>Recipe Results:</h1>
				{/* {reviews} */}
				{/* <button onClick={onClickSave}>Save Recipes</button> */}
			</div>
		);
	}
}

export default App;
