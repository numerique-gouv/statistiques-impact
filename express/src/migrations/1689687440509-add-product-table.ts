import { MigrationInterface, QueryRunner } from "typeorm";

export class AddProductTable1689687440509 implements MigrationInterface {
    name = 'AddProductTable1689687440509'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "product" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "name" character varying NOT NULL, CONSTRAINT "PK_bebc9158e480b949565b4dc7a82" PRIMARY KEY ("id"))`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "nom_service_public_numerique"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "productId" uuid`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "date"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "date" character varying NOT NULL`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD CONSTRAINT "One unique value for indicator by frequence and date" UNIQUE ("productId", "indicateur", "frequence_calcul", "date")`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD CONSTRAINT "FK_aa15d700b2d58418a05c65c071f" FOREIGN KEY ("productId") REFERENCES "product"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "indicator" DROP CONSTRAINT "FK_aa15d700b2d58418a05c65c071f"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP CONSTRAINT "One unique value for indicator by frequence and date"`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "date"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "date" TIMESTAMP WITH TIME ZONE NOT NULL`);
        await queryRunner.query(`ALTER TABLE "indicator" DROP COLUMN "productId"`);
        await queryRunner.query(`ALTER TABLE "indicator" ADD "nom_service_public_numerique" character varying NOT NULL`);
        await queryRunner.query(`DROP TABLE "product"`);
    }

}
