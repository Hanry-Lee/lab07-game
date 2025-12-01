# Game State Specification

## player.csv
### File: required
#### Primary key (player_id)
| Field Name | Type          | Presence | Description |
| ---------- | ------------- | -------- | ----------- |
| player_id  | Unique ID     | Required | A unique ID for the player or opponent. |
| x          | Screen X      | Required | The x-position of the player on screen. |
| y          | Screen Y      | Required | The y-position of the player on screen. |
| size       | Positive Int  | Required | The size/radius of the player. |
| speed      | Positive Float| Required | The movement speed of the player. |
| color      | Color         | Required | The color of the player. |
| count      | Positive Int  | Required | The number of food items eaten. |

## food.csv
### File: required
#### Primary key (food_id)
| Field Name | Type         | Presence | Description |
| ---------- | ------------ | -------- | ----------- |
| food_id    | Unique ID    | Required | A unique ID for every food item. |
| x          | Screen X     | Required | The x-position of the food on screen. |
| y          | Screen Y     | Required | The y-position of the food on screen. |
| size       | Positive Int | Required | The size/radius of the food. |

## Field Types

- **Unique ID**: An ID field value is an internal ID, not intended to be shown to players, and is a sequence of any UTF-8 characters. Using only printable ASCII characters is recommended. An ID is labeled "unique ID" when it must be unique within a file.

- **Screen X**: A float between 0 and Screen Width (1280).

- **Screen Y**: A float between 0 and Screen Height (720).

- **Screen Width**: 1280 pixels (game window width).

- **Screen Height**: 720 pixels (game window height).

- **Positive Int**: A non-negative integer (0 or greater).

- **Positive Float**: A non-negative float (0.0 or greater).

- **Color**: A valid color name string. Supported colors: red, blue, green, yellow, white, black, orange, purple, pink, cyan, magenta, gray.

## Example Data

### player.csv
```
player_id,x,y,size,speed,color,count
player1,100,200,10,5.0,red,3
opponent1,300,400,15,3.0,blue,5
```

### food.csv
```
food_id,x,y,size
food1,100,200,10
food2,500,300,10
food3,800,600,10
```
